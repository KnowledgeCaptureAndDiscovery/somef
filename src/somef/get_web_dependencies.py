import json
import xml.etree.ElementTree as ET

def check_web_dependencies_requirements(file_path):
    web_dependencies = ['Flask', 'Django', 'React', 'Angular', 'Vue.js', 'Express.js',
                        'Bootstrap', 'jQuery', 'Sass', 'Babel']
    found_dependencies = []
    
    with open(file_path, 'r') as requirements_file:
        for line in requirements_file:
            line = line.strip()
            
            if not line or line.startswith('#'):
                continue

            for dependency in web_dependencies:
                if dependency in line:
                    found_dependencies.append(dependency)
    
    return found_dependencies

import json
import xml.etree.ElementTree as ET

def get_web_dependencies(repository_file_path):
    web_dependencies = []
    dependency_keys = {
        'package.json': ('npm', 'dependencies'),
        'requirements.txt': ('pip', 'dependencies'),
        'composer.json': ('composer', 'require'),
        'Gemfile': ('Gemfile', 'gem'),
        'pom.xml': ('pom.xml', 'dependencies')
    }

    package_manager = None
    dependency_key = None

    for file_name, (pm, key) in dependency_keys.items():
        if file_name in repository_file_path:
            package_manager = pm
            dependency_key = key
            break

    if package_manager is not None and dependency_key is not None:
        with open(repository_file, 'r') as f:
            if package_manager == 'pom.xml':
                tree = ET.parse(repository_file)
                root = tree.getroot()
                namespaces = {'ns': 'http://maven.apache.org/POM/4.0.0'}

                # Add website/web application dependencies
                website_frameworks = {
                    'org.springframework.boot': 'Spring Boot',
                    'javax.servlet': 'Java Servlet API',
                    'org.hibernate': 'Hibernate',
                    'express.js': 'Express.js',
                    'react.js': 'React.js',
                    'angular.js': 'Angular.js',
                    'vue.js': 'Vue.js',
                    'django': 'Django',
                    'flask': 'Flask',
                    'fastapi': 'FastAPI',
                    'laravel': 'Laravel',
                    'symfony': 'Symfony',
                    'codeigniter': 'CodeIgniter',
                    'ruby on rails': 'Ruby on Rails',
                    'sinatra': 'Sinatra',
                    'asp.net': 'ASP.NET',
                    'entity framework': 'Entity Framework'
                }

                for dependency in root.findall('.//ns:dependency', namespaces):
                    group_id = dependency.find('ns:groupId', namespaces).text
                    artifact_id = dependency.find('ns:artifactId', namespaces).text
                    dependency_key = f'{group_id}:{artifact_id}'
                    
                    if group_id in website_frameworks:
                        web_dependencies.append(website_frameworks[group_id])
                    elif dependency_key in website_frameworks:
                        web_dependencies.append(website_frameworks[dependency_key])
            
                return web_dependencies
            else:
                data = json.load(f)
                if dependency_key in data:
                    if package_manager == 'npm':
                        if 'react' in data[dependency_key]:
                            web_dependencies.append('React')
                        if 'angular' in data[dependency_key]:
                            web_dependencies.append('Angular')
                        if 'vue' in data[dependency_key]:
                            web_dependencies.append('Vue.js')
                    elif package_manager == 'pip':
                        if 'Django' in data[dependency_key]:
                            web_dependencies.append('Django')
                        if 'Flask' in data[dependency_key]:
                            web_dependencies.append('Flask')
                        if 'FastAPI' in data[dependency_key]:
                            web_dependencies.append('FastAPI')
                    elif package_manager == 'composer':
                        if 'laravel/framework' in data[dependency_key]:
                            web_dependencies.append('Laravel')
                        if 'symfony/framework-bundle' in data[dependency_key]:
                            web_dependencies.append('Symfony')
                        if 'cakephp/cakephp' in data[dependency_key]:
                            web_dependencies.append('CakePHP')
                    elif package_manager == 'Gemfile':
                        if 'rails' in data[dependency_key]:
                            web_dependencies.append('Ruby on Rails')
                        if 'sinatra' in data[dependency_key]:
                            web_dependencies.append('Sinatra')
                        if 'padrino' in data[dependency_key]:
                            web_dependencies.append('Padrino')

    return web_dependencies

