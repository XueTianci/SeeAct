# Disclaimer: this is not a functional agent and is only for demonstration purposes. This implementation is just a single model call.
from src.seeact import run_single_task
import os
import toml
import asyncio

def run(input: dict[str, dict], **kwargs) -> dict[str, str]:

    assert 'model_name' in kwargs, 'model_name is required'
    assert len(input) == 1, 'input must contain only one task'

    print(kwargs)
    # Load configuration file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config = None
    try:
        with open(os.path.join(base_dir, kwargs["config_path"]) if not os.path.isabs(kwargs["config_path"]) else kwargs["config_path"],
                  'r') as toml_config_file:
            config = toml.load(toml_config_file)
            print(f"Configuration File Loaded - {os.path.join(base_dir, kwargs["config_path"])}")
    except FileNotFoundError:
        print(f"Error: File '{kwargs["config_path"]}' not found.")
    except toml.TomlDecodeError:
        print(f"Error: File '{kwargs["config_path"]}' is not a valid TOML file.")

    config["api_parameter"]["model"] = kwargs["model_name"]
    # config["openai"]["api_key"] = os.getenv("OPENAI_API_KEY", None)

    task_id, task = list(input.items())[0]
    task["task_id"] = task_id
    print(f"Task ID: {task_id}")
    print(f"Task: {task}")

    asyncio.run(run_single_task(task_id, task, config, base_dir))
    
    results = {}
    results[task_id] = {"trajectory": f"./results/online_mind2web/RUN_ID/{task_id}/result/trajectory", 
                        "result_file": f"./results/online_mind2web/RUN_ID/{task_id}/result/result.json"}
    
        
    return results