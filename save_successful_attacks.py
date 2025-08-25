import os
import json
from datetime import datetime

def save_successful_attacks(target_llm_ar, instruct, full_instruct, jailbroken_list, test_prefixes, save_dir="successful_attacks"):
    """
    Args:
        target_llm_ar
        instruct: original prompt
        full_instruct
        jailbroken_list: if the attack was successful
        test_prefixes
        save_dir
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    successful_attacks = []
    for i, is_success in enumerate(jailbroken_list):
        if is_success:
            attack = {
                "original_prompt": instruct.text[i],
                "attack_prompt": full_instruct.text[i],
                "model_response": target_llm_ar.response_sample.text[i],
                "test_prefixes": test_prefixes,
                "timestamp": timestamp
            }
            successful_attacks.append(attack)
    
    if successful_attacks:
        output_file = os.path.join(save_dir, f"successful_attacks_{timestamp}.json")
        with open(output_file, "w") as f:
            json.dump(successful_attacks, f, indent=2)
        print(f"Saved {len(successful_attacks)} successful attacks to {output_file}")
        
        # create report
        report_file = os.path.join(save_dir, f"attack_report_{timestamp}.txt")
        with open(report_file, "w") as f:
            f.write(f"Attack Report - {timestamp}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total successful attacks: {len(successful_attacks)}\n\n")
            for i, attack in enumerate(successful_attacks, 1):
                f.write(f"Attack #{i}\n")
                f.write("-" * 30 + "\n")
                f.write(f"Original prompt: {attack['original_prompt']}\n")
                f.write(f"Attack prompt: {attack['attack_prompt']}\n")
                f.write(f"Model response: {attack['model_response']}\n\n")
