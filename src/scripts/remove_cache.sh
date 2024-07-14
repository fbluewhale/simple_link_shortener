find . | grep -E "(/__pycache__$|\.pyc$|\.pytest_cache$)" | xargs rm -rf
