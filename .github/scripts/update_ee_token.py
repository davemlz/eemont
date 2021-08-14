import os

# Token from SECRETS
credentials = '{"refresh_token":"%s"}' % os.environ["EE_TOKEN"]
# We need this location to save the token
credentialsPath = os.path.expanduser("~/.config/earthengine/")
os.makedirs(credentialsPath, exist_ok=True)
# Write the token
with open(credentialsPath + "credentials", "w") as f:
    f.write(credentials)
