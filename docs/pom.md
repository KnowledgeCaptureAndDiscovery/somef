The following metadata fields can be extracted from a pom.xml file.   
These fields are defined in the [Maven POM specification](https://maven.apache.org/pom.html), currently at version **4.0.0**, and are mapped according to the [CodeMeta crosswalk for Java (Maven)](https://github.com/codemeta/codemeta/blob/master/crosswalks/Java%20(Maven).csv).

| Software metadata category       |   SOMEF metadata JSON path                 | POM.XML metadata file field    |
|-------------------------------|---------------------------------------------|----------------------------------|
| authors - value                   |  authors[i].result.value       |    developers.developer.name |
| authors - name                   |  authors[i].result.name       |     developers.developer.name |
| authors - email                   |  Aauthors[i].result.email      |     developers.developer.email |
| authors - url                   |  authors[i].result.url         |     developers.developer.url |
| authors - affiliation                   |  authors[i].result.affiliation |     developers.developer.organization |
| has_package_file          | has_package_file[i].result .value      |  URL of the pom.xml file |
| homepage                  |  homepage[i].result.value | homepage |
| issue_tracker             | issue_tracker[i].result .value    | issueManagement.url                  |
| package_distribution - value      |    package_distribution[i].result value  | scm.url *(1)*|
| package_distribution - value      |    package_distribution[i].result.value   | repositories.repository(id) *(2)*|
| package_distribution - name      |    package_distribution[i].result.name   | repositories.repository(name) *(2)*|
| package_distribution - url      |    package_distribution[i].result.url  | repositories.repository(url) *(2)*|
| requirements - value             |   requirements[i].result.value   | dependencies.dependency.grpId.arfifactId  *(3)*                        |
| requirements - name            |   requirements[i].result.name  | dependencies.dependency.arfifactId    *(3)*                     |
| requirements - version              |   requirements[i].result.version   | dependencies.dependency.version    *(3)*                    |
| package_id                 |   package_id[i].result .value   | group_id.artifact_id             *(4)*              |
| runtime_platform - value          |    runtime_platform[i].result.value |  properties  extract name version  *(5)*  |
| runtime_platform - name          |    runtime_platform[i].result.name |   properties extract name    *(5)*|
| runtime_platform - value          |   runtime_platform[i].result.value |  properties  extract version  *(5)*  |
| version                   |  version[i].result .value  | version                    |

---

*(1)*  
- Example:
```
  <scm>
    <connection>scm:svn:http://127.0.0.1/svn/my-project</connection>
    <developerConnection>scm:svn:https://127.0.0.1/svn/my-project</developerConnection>
    <tag>HEAD</tag>
    <url>http://127.0.0.1/websvn/my-project</url>
  </scm>
```
- Result: 
```
package_distribution': [{'result': {'value': 'http://127.0.0.1/websvn/my-project', 'type': 'Url'}, 'confidence': 1, 'technique': 'code_parser', 'source': 'https://example.org/pom.xml'}]
```

*(2)*  
- Example:
```
</repositories>
    <repository>
        <id>jitpack.io</id>
        <url>https://jitpack.io</url>
    </repository>
</repositories>
```
- Result:
```
'package_distribution': [{
    'result': {
        'value': 'jitpack.io', 
        'url': 'https://jitpack.io', 
        'type': 'Url'
    }
```

*(3)*  
- Example:
```
	<dependencies>
		<dependency>
			<groupId>org.apache.maven</groupId>
			<artifactId>maven-model</artifactId>
			<version>3.9.0</version>
		</dependency>
    </dependencies>

```
- Result:
```
'requirements': [{
    'result': 
        {'value': 'org.apache.maven.maven-model', 
        'name': 'maven-model', 
        'version': '3.9.0', 
        'type': 'Software_application'}, 

```

*(4)*  
- Example:
```
	<groupId>es.oeg</groupId>
	<artifactId>widoco</artifactId>
 ```  
- Result:
```
 'package_id': [{
    'result': {
        'value': 'es.oeg.widoco', 

``` 

 *(5)*
 - Example:
```
	<properties>
		<java.version>1.8</java.version>
	</properties>
```

- Result:
```
[{'value': 'Java: 1.8', 'name': 'Java', 'version': '1.8'}]
```
