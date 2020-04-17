from setuptools import setup

setup(
    name='WeatherPlot',
    version='1.0',
    description=" python final project",
    author='Patrick Jiang',
    author_email='patrick.jiang86@gmail.com',
    url='https://patrick-jiang.github.io/',
    py_modules=[
        'weather_processor,db_context_manager,db_operations,plot_operations,scrape_weather'],
)
