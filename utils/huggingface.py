"""
"""

from exceptions.exceptions import WrongInstanceType


def load_model_and_processor(model_module_name, processor_module_name, cache_dir=None):
    """
    """
    try:
        model_str = "/".join(model_module_name.split("/")[1:])
        model_module_str = model_module_name.split("/")[0]
        model_module = getattr(
            __import__('transformers', fromlist=[model_module_str]), model_module_str
            )
        model = getattr(model_module, "from_pretrained")(
            model_str, cache_dir=cache_dir)


        processor_str = "/".join(processor_module_name.split("/")[1:])
        processor_module_str = processor_module_name.split("/")[0]
        processor_module = getattr(
            __import__('transformers', fromlist=[processor_module_str]), processor_module_str
            )
        processor = getattr(processor_module, "from_pretrained")(
            processor_str, cache_dir=cache_dir)
        
        return model, processor
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Error loading module or model: {e}")
        return None


def vectorize_image(model, processor, image_dict):
    """
    """
    if not isinstance(image_dict, dict):
        raise WrongInstanceType(
            f"`image_dict` type should be `dict`, recieved: {type(image_dict)}"
            )

    inputs = processor(images=image_dict['image'], return_tensors="pt")
    try:
        outputs = model.get_image_features(**inputs)
    except:
        outputs = model(**inputs).last_hidden_state

    image_dict["image_vectorized"] = outputs[0].detach().numpy()

    return image_dict


def convert_text_to_diagnosis(image_batch):
    """
    Preprocesses a batch of images, converting images and generating one-hot encoded labels.
    """
 
    diagnosis_list = []

    for example in image_batch['text']:
        diagnoses = example.replace("'", "").split('; ')[1:]
        
        for i, diagnose in enumerate(diagnoses):
            if not diagnose:
                diagnose = "Stable with Minor Abnormalities"
                
            diagnoses[i] = diagnose
            
            
        diagnosis_list.append(diagnoses)

    image_batch['diagnoses'] = diagnosis_list
    return image_batch