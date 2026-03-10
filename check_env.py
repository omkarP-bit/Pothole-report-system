import os

def check_env_vars():
    print("🔍 Checking Environment Variables...\n")
    
    # Check Supabase
    supabase_url = os.getenv('SUPABASE_DB_URL')
    if supabase_url:
        print(f"✅ SUPABASE_DB_URL: {supabase_url[:50]}...")
        if 'supabase.com' in supabase_url and 'postgresql://' in supabase_url:
            print("✅ URL format looks correct")
        else:
            print("⚠️ URL format might be incorrect")
    else:
        print("❌ SUPABASE_DB_URL not found")
    
    print()
    
    # Check AWS
    aws_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_BUCKET_NAME', 'AWS_REGION']
    aws_ok = True
    
    for var in aws_vars:
        value = os.getenv(var)
        if value:
            if 'SECRET' in var:
                print(f"✅ {var}: {value[:10]}...")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not found")
            aws_ok = False
    
    print()
    
    # Check Flask
    secret_key = os.getenv('SECRET_KEY')
    if secret_key:
        print(f"✅ SECRET_KEY: {secret_key[:10]}...")
    else:
        print("❌ SECRET_KEY: Not found")
    
    print(f"\n📊 Summary:")
    print(f"Database Config: {'✅' if supabase_url else '❌'}")
    print(f"AWS Config: {'✅' if aws_ok else '❌'}")
    print(f"Flask Config: {'✅' if secret_key else '❌'}")

if __name__ == "__main__":
    # Load from .env file manually
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"')
        print("📁 Loaded .env file\n")
    except FileNotFoundError:
        print("⚠️ No .env file found, checking system environment\n")
    
    check_env_vars()