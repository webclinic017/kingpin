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

- 6、Debian系统 sans-serif 字体缺失，plot无法显示中文
    - [SimHei 下载地址](http://www.fontpalace.com/font-download/simhei)
    - 获取对应字体文件夹路径
        - python -c "import matplotlib as p;print(p.matplotlib_fname())"
        - 根据mpl-data路径找到 mpl-data/fonts/ttf
        - 把字体文件copy至ttf目录
    - 删除matplotlib缓存
        - python -c "import matplotlib as p;print(p.get_cachedir())"
        - rm -rf cache_path
    - 修改matplotlibrc文件
        - 根据mpl-data路径找打 mpl-data/matplotlibrc 
        - vim mpl-data/matplotlibrc
        > \# 修改的内容

        > font.family: sans-serif

        > \# 去掉前面的#，并在冒号后面添加SimHei

        > font.sans-serif : SimHei, DejaVu Sans, Bitstream Vera Sans, Computer Modern Sans Serif, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif
        
        > \# 去掉前面的#，并将True改为False
        
        > axes.unicode_minus  : False
        

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

