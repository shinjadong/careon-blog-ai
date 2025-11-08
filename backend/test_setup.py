"""
Quick setup test script
Tests if all dependencies are installed and ADB is working
"""
import sys


def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing package imports...")

    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("sqlalchemy", "SQLAlchemy"),
        ("pydantic", "Pydantic"),
        ("adbutils", "ADBUtils"),
        ("PIL", "Pillow"),
        ("loguru", "Loguru"),
    ]

    failed = []
    for package, name in packages:
        try:
            __import__(package)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - NOT INSTALLED")
            failed.append(name)

    if failed:
        print(f"\n❌ Missing packages: {', '.join(failed)}")
        print("\n💡 Run: pip install -r requirements.txt")
        return False

    print("\n✅ All packages imported successfully!")
    return True


def test_adb_connection():
    """Test ADB connection"""
    print("\n🔍 Testing ADB connection...")

    try:
        from adbutils import adb

        # Try to connect to ADB server
        devices = adb.device_list()

        if not devices:
            print("  ⚠️  No ADB devices found")
            print("\n💡 Make sure:")
            print("  1. Android device is connected via USB")
            print("  2. USB debugging is enabled")
            print("  3. ADB is installed and accessible")
            print("  4. Run 'adb devices' in terminal to verify")
            return False

        print(f"  ✅ Found {len(devices)} ADB device(s):")
        for device in devices:
            print(f"    - {device.serial}")

        return True

    except Exception as e:
        print(f"  ❌ ADB connection failed: {e}")
        return False


def test_database():
    """Test database initialization"""
    print("\n🔍 Testing database setup...")

    try:
        from app.core.database import init_db, engine

        init_db()
        print("  ✅ Database initialized successfully")

        # Test connection
        with engine.connect() as conn:
            print("  ✅ Database connection successful")

        return True

    except Exception as e:
        print(f"  ❌ Database test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("CareOn Blog Automation - Setup Test")
    print("=" * 60)

    results = []

    # Test 1: Imports
    results.append(test_imports())

    # Test 2: ADB
    results.append(test_adb_connection())

    # Test 3: Database
    results.append(test_database())

    # Summary
    print("\n" + "=" * 60)
    if all(results):
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Setup is complete. You can now run:")
        print("   uvicorn main:app --reload")
        print("\n📚 API docs will be available at:")
        print("   http://localhost:8000/docs")
    else:
        print("❌ SOME TESTS FAILED")
        print("\n💡 Please fix the issues above before starting the server")

    print("=" * 60)

    return all(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
