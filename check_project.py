"""
项目完整性检查脚本
检查所有必需的文件和配置
"""

import os
import sys

def check_file(filepath, required=True):
    """检查文件是否存在"""
    exists = os.path.exists(filepath)
    status = "✓" if exists else ("✗" if required else "⚠")
    print(f"{status} {filepath}")
    return exists

def check_directory(dirpath, create=True):
    """检查目录是否存在"""
    exists = os.path.exists(dirpath)
    if not exists and create:
        os.makedirs(dirpath, exist_ok=True)
        print(f"✓ {dirpath} (已创建)")
        return True
    elif exists:
        print(f"✓ {dirpath}")
        return True
    else:
        print(f"✗ {dirpath}")
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✓ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python版本过低: {version.major}.{version.minor}.{version.micro} (需要 3.9+)")
        return False

def check_imports():
    """检查关键依赖包"""
    packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_jwt_extended',
        'flask_cors',
        'werkzeug',
        'PIL',
        'cv2',
        'numpy'
    ]
    
    print("\n检查Python包:")
    all_ok = True
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (未安装)")
            all_ok = False
    
    return all_ok

def main():
    """主检查函数"""
    print("=" * 50)
    print("命运预测系统 - 项目完整性检查")
    print("=" * 50)
    print()
    
    # 检查Python版本
    print("检查Python版本:")
    python_ok = check_python_version()
    print()
    
    # 检查核心文件
    print("检查核心文件:")
    files_ok = all([
        check_file('app.py'),
        check_file('run.py'),
        check_file('config.py'),
        check_file('init_db.py'),
        check_file('requirements.txt'),
        check_file('.env.example'),
        check_file('.env', required=False)
    ])
    print()
    
    # 检查models目录
    print("检查models目录:")
    models_ok = all([
        check_directory('models'),
        check_file('models/__init__.py'),
        check_file('models/user.py'),
        check_file('models/prediction.py')
    ])
    print()
    
    # 检查services目录
    print("检查services目录:")
    services_ok = all([
        check_directory('services'),
        check_file('services/__init__.py'),
        check_file('services/image_processor.py'),
        check_file('services/personality_analyzer.py'),
        check_file('services/career_predictor.py'),
        check_file('services/wealth_predictor.py'),
        check_file('services/love_analyzer.py'),
        check_file('services/fortune_analyzer.py'),
        check_file('services/astrology_analyzer.py')
    ])
    print()
    
    # 检查必要目录
    print("检查必要目录:")
    dirs_ok = all([
        check_directory('static'),
        check_directory('static/uploads'),
        check_directory('logs'),
        check_directory('backups'),
        check_directory('tests')
    ])
    print()
    
    # 检查依赖包
    imports_ok = check_imports()
    print()
    
    # 检查配置文件
    print("检查配置:")
    if not os.path.exists('.env'):
        print("⚠ .env文件不存在")
        print("  建议: cp .env.example .env")
        config_ok = False
    else:
        print("✓ .env文件存在")
        config_ok = True
    print()
    
    # 总结
    print("=" * 50)
    print("检查总结:")
    print("=" * 50)
    
    all_checks = {
        'Python版本': python_ok,
        '核心文件': files_ok,
        'Models模块': models_ok,
        'Services模块': services_ok,
        '目录结构': dirs_ok,
        'Python依赖': imports_ok,
        '配置文件': config_ok
    }
    
    for check_name, result in all_checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check_name}")
    
    print()
    
    if all(all_checks.values()):
        print("🎉 所有检查通过！项目已准备就绪。")
        print()
        print("下一步:")
        print("1. 编辑.env文件，设置密钥")
        print("2. 运行: python init_db.py")
        print("3. 运行: python run.py")
        return 0
    else:
        print("❌ 存在问题，请先解决上述错误。")
        print()
        print("建议:")
        if not python_ok:
            print("- 升级Python到3.9或更高版本")
        if not imports_ok:
            print("- 运行: pip install -r requirements.txt")
        if not config_ok:
            print("- 运行: cp .env.example .env")
        return 1

if __name__ == '__main__':
    sys.exit(main())