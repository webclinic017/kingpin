# kingpin
拱门爸比的数据脚本

## 开发环境Tips
- 1、创建conda env环境
    - conda create -n kingpin python=$\color{#4285f4}{3.10}$
- 2、切换conda env
    - conda activate env_name
- 3、安装项目依赖
    - cd workspace/kingpin/
    - python -m pip install -r requirements.txt

- 4、安装第三方or自定义packages
    - cd ./packages/package_name
    - python -m pip install -e .
    - #e=editable 既修改package代码也能生效

- 5、命令行运行忽略 ignore信息
    - python -W ignore file.py

## VSC 配置
- 1、工作区下配置文件 
    - .vscode/settings.json
- 2、解决conda python地址
    - 配置选项 "python.defaultInterpreterPath": "your_conda_env_python_path"
- 3、解决安装包之后pylance找不到提示信息
    - 配置选项 "python.analysis.extraPaths": [ "your_conda_env_pip_packages_path" ]

## Git 配置
- 1、忽略提交某些个人配置文件
    - 配置文件 .gitignore
    - 添加
        - .vscode/
        - .github/

## CUDA 
- 1、安装（对应conda env环境)
    - conda install cudatoolkit
    - conda install cudnn
- 2、验证安装成功
    
    `#python`

    `import totch`

    `print(torch.cuda.is_avable())`

