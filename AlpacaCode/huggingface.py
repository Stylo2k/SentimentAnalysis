from huggingface_hub import notebook_login
 
notebook_login()
 
model.push_to_hub("moalshak/alpaca-commits-sentiment", use_auth_token=True)