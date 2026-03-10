import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine, text

load_dotenv()

def test_supabase_connection():
    db_url = os.getenv('SUPABASE_DB_URL')
    
    if not db_url:
        print("❌ SUPABASE_DB_URL not found in environment")
        return False
    
    print(f"🔗 Testing connection to: {db_url[:50]}...")
    
    try:
        # Test with SQLAlchemy (Flask-SQLAlchemy compatible)
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ SQLAlchemy connection successful!")
            print(f"📊 PostgreSQL version: {version[:50]}...")
        
        # Test basic query
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"))
            table_count = result.fetchone()[0]
            print(f"📋 Found {table_count} tables in public schema")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def test_aws_credentials():
    aws_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
    bucket = os.getenv('AWS_BUCKET_NAME')
    
    if not all([aws_key, aws_secret, bucket]):
        print("❌ AWS credentials incomplete")
        return False
    
    print(f"🔑 AWS Key: {aws_key[:10]}...")
    print(f"🪣 S3 Bucket: {bucket}")
    
    try:
        import boto3
        s3 = boto3.client('s3', 
                         aws_access_key_id=aws_key,
                         aws_secret_access_key=aws_secret,
                         region_name=os.getenv('AWS_REGION'))
        
        # Test bucket access
        s3.head_bucket(Bucket=bucket)
        print("✅ AWS S3 connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ AWS S3 connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Environment Connections...\n")
    
    db_ok = test_supabase_connection()
    print()
    aws_ok = test_aws_credentials()
    
    print(f"\n📊 Results:")
    print(f"Database: {'✅' if db_ok else '❌'}")
    print(f"AWS S3: {'✅' if aws_ok else '❌'}")
    
    if db_ok and aws_ok:
        print("\n🎉 All connections working! Ready for hackathon!")
    else:
        print("\n⚠️ Fix connection issues before proceeding")