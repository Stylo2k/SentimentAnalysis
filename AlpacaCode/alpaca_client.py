from gradio_client import Client

client = Client("https://bd1433e4dd6dfb2565.gradio.live/")

import json
data = json.load(open("alpaca_dataset_v2.json"))

starting_index = 0
index = 0

for d in data:
    if index < starting_index:
        index += 1
        continue
    print(index)
    result = client.predict(
                    f"{d['instruction']}",	# str in 'Instruction' Textbox component
                    f"{d['input']}",	# str in 'Input' Textbox component
                    0.1,	# int | float (numeric value between 0 and 1) in 'Temperature' Slider component
                    0.5,	# int | float (numeric value between 0 and 1) in 'Top p' Slider component
                    40,	# int | float (numeric value between 0 and 100) in 'Top k' Slider component
                    4,	# int | float (numeric value between 1 and 4) in 'Beams' Slider component
                    128,	# int | float (numeric value between 1 and 2000) in 'Max tokens' Slider component,
                    False,
                    api_name="/predict"
    )
    d['alpaca_output'] = result
    file_name = "llama_with_dataset.json"
    json.dump(data, open(file_name, "w"), indent=4)
    
