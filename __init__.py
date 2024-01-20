from invokeai.app.invocations.primitives import (
    ImageField,
    ImageOutput,
    ColorField,
)
from invokeai.app.services.image_records.image_records_common import ImageCategory, ResourceOrigin

from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    Input,
    InputField,
    InvocationContext,
    invocation,
)
import colorsys
from PIL import Image
import numpy as np

@invocation(
    "distance_desaturation",
    title="Exponential Distance Desaturation",
    tags=["image", "color", "desaturation"],
    category="image",
    version="1.0.0",
)
class ExponentialDesaturationInvocation(BaseInvocation):
    """
    Desaturate colors close to a target hue
    """
    image: ImageField = InputField(
        title="Image",
        description="Image to desaturate",
    )
    color: ColorField = InputField(
        title="Color",
        description="Color to desaturate",
        input=Input.Connection,
    )
    strength: float = InputField(
        title="Strength",
        description="How strongly to apply the desaturation",
        le=1,
        ge=0,
        default=1,
        )
    exponent: float = InputField(
        title="Exponent",
        description="Affects how close to the selected color the desaturation will be applied",
        ge=1,
        default=10,
        )
    preserve_luminosity: bool = InputField(
        title="Preserve Luminosity",
        description="Preserve the luminosity of the image",
        default=False,
        )
    invert_result: bool = InputField(
        title="Invert Result",
        description="Preserve the target color instead of desaturating it",
        default=False,
        )

    def invoke(self, context: InvocationContext) -> ImageOutput:
        image = context.services.images.get_pil_image(self.image.image_name)
        color = self.color.tuple()
        saturation_target = 1 - self.strength

        #get the luminosity channel of the original input image as a numpy array
        """ NOTE: PIL likes to pretend that it can't convert from RGB to LAB, but it can.
        It just doesn't want to, and it has a check to make sure the program doesn't have "LAB" hardcoded as a literal in the convert() method.
        For whatever bonkers reason, making a variable that is equal to "LAB" and passing that in as the mode works just fine.
        """
        mode="LAB"
        original_luminosity = np.array(image.convert(mode)).astype(np.uint8)[:, :, 0]


        # Convert the image to HSV
        image = image.convert("HSV")
        #scale the values to be between 0 and 1 instead of 0 and 255
        image = np.array(image) / 255

        # Convert the color to HSV
        color = colorsys.rgb_to_hsv(color[0] / 255, color[1] / 255, color[2] / 255)

        # Adjust the Saturation channel based on the distance squared between the Hue and the hue of the color input
        hue_difference = np.abs(image[:, :, 0] - color[0])
        hue_difference = np.minimum(hue_difference, 1 - hue_difference) # wrap around the hue circle, so that the hue difference is always between 0 and 0.5
        hue_scaling = (1 - (2 * hue_difference)) ** self.exponent # scale the hue difference so that it is 1 near the target hue and 0 far away
        if self.invert_result:
            hue_scaling = 1 - hue_scaling
        image[:, :, 1] = image[:, :, 1] * (saturation_target * hue_scaling + (1 - hue_scaling))

        # Convert the image back to RGB
        image = Image.fromarray((image * 255).astype(np.uint8), mode="HSV")
        
        image = image.convert("RGB")

        # replace the luminosity 
        if self.preserve_luminosity:
            lab_image = np.array(image.convert(mode)).astype(np.uint8)
            lab_image[:, : ,0] = original_luminosity
            image = Image.fromarray(lab_image, mode=mode).convert("RGB")

        image_dto = context.services.images.create(
            image=image,
            image_origin=ResourceOrigin.INTERNAL,
            image_category=ImageCategory.GENERAL,
            node_id=self.id,
            session_id=context.graph_execution_state_id,
            is_intermediate=self.is_intermediate,
            workflow=context.workflow,
        )

        return ImageOutput(
            image=ImageField(image_name=image_dto.image_name),
            width=image.width,
            height=image.height,
        )