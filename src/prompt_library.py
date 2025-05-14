

class PromptLibrary:
    default_prompt = """
Parse this DME doctor request and format as json. Here are some examples.

Input Examples
Use these sample texts and try to extract structured data using your prompt.
Input Text:  Patient requires a full face CPAP mask with humidifier due to AHI > 20. Ordered by Dr. Cameron.
Target Output: json {   "device": "CPAP",   "mask_type": "full face",   "add_ons": ["humidifier"],   "qualifier": "AHI > 20",   "ordering_provider": "Dr. Cameron" } 

Input Text:  Patient diagnosed with COPD, SpO2 measured at 87% on room air. Needs portable oxygen concentrator for use during exertion and sleep. Dr. Chase signed the order.  
Target Output: json {   "device": "portable oxygen concentrator",   "diagnosis": "COPD",   "SpO2": "87%",   "usage": ["exertion", "sleep"],   "ordering_provider": "Dr. Chase" } 

Input Text:  Patient has MS with significant mobility issues. Recommended a lightweight manual wheelchair with elevating leg rests. Ordered by Dr. Taub.  
Target Output: json {   "device": "manual wheelchair",   "type": "lightweight",   "features": ["elevating leg rests"],   "diagnosis": "MS",   "ordering_provider": "Dr. Taub" } 

Input Text:  Asthma diagnosis confirmed. Prescribing nebulizer with mouthpiece and tubing. Dr. Foreman completed the documentation.  
Target Output: json {   "device": "nebulizer",   "accessories": ["mouthpiece", "tubing"],   "diagnosis": "Asthma",   "ordering_provider": "Dr. Foreman" } 

Input Text:  Patient is non-ambulatory and requires hospital bed with trapeze bar and side rails. Diagnosis: late-stage ALS. Order submitted by Dr. Cuddy.  
Target Output: json {   "device": "hospital bed",   "features": ["trapeze bar", "side rails"],   "diagnosis": "ALS",   "mobility_status": "non-ambulatory",   "ordering_provider": "Dr. Cuddy" }

Input Text:  CPAP supplies requested. Full face mask with headgear and filters. Patient has been compliant. Ordered by Dr. House.  
Target Output: json {   "product": "CPAP supplies",   "components": ["full face mask", "headgear", "filters"],   "compliance_status": "compliant",   "ordering_provider": "Dr. House" }

"""


class PromptPrep:
    max_prompt_token_length_o1mini = 128000

    @staticmethod
    def estimate_tokens(prompt: str) -> int:
        """Estimate the number of tokens in a string."""
        tokens_per_char = 0.25  # rough estimate of tokens per character for English text
        return int(len(prompt) * tokens_per_char)