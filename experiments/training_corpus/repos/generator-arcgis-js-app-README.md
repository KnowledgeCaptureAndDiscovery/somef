[![Build Status](https://travis-ci.org/odoe/generator-arcgis-js-app.svg?branch=master)](https://travis-ci.org/odoe/generator-arcgis-js-app)
[![Dependencies Status](https://david-dm.org/odoe/generator-arcgis-js-app.svg)](https://david-dm.org/odoe/generator-arcgis-js-app)
# generator-arcgis-js-app

> [Yeoman](http://yeoman.io) generator

This is a yeoman generator for [ArcGIS API for JavaScript applications](https://developers.arcgis.com/javascript/).

## Getting Started

### What is Yeoman?

Trick question. It's not a thing. It's this guy:

![](http://i.imgur.com/JHaAlBJ.png)

Basically, he wears a top hat, lives in your computer, and waits for you to tell him what kind of application you wish to create.

Not every new computer comes with a Yeoman pre-installed. He lives in the [npm](https://npmjs.org) package repository. You only have to ask for him once, then he packs up and moves into your hard drive. *Make sure you clean up, he likes new and shiny things.*

```bash
npm install -g yo
npm install -g bower
```

Bower is a required dependency of using the packages in the generated app.

### Yeoman Generators

Yeoman travels light. He didn't pack any generators when he moved in. You can think of a generator like a plug-in. You get to choose what type of application you wish to create, such as a Backbone application or even a Chrome extension.

To install generator-arcgis-js-app from npm, run:

```bash
npm install -g generator-arcgis-js-app
```

Finally, initiate the generator inside application folder:

```bash
yo arcgis-js-app
```

or

```bash
yo arcgis-js-app application-name
```

You will be asked:
* Application name if not provided
* Description of application
* ArcGIS API Version (3.x or 4.x)
* Use Stylus or Sass
* Email to be used in package information

Will create component and tests. Updates `intern.js` with test suite.


### What is used?
* New use 3.x or 4.x of the [ArcGIS API for JavaScript](https://developers.arcgis.com/javascript/)
* Output application uses [GruntJS](http://gruntjs.com/) for running tasks
* All code is written in [ES6/ES2015](https://github.com/lukehoban/es6features) and transpiled with [babel](https://babeljs.io/)
* Uses [eslint](https://github.com/eslint/eslint) to lint code
* Uses [stylus](https://learnboost.github.io/stylus/) or [sass](http://sass-lang.com/) as a css preprocessor
* Uses [livereload](http://livereload.com/) for easier development workflow

### Usage

`grunt` - default task, will output code to a `dist` folder with sourcemaps.

`grunt dev` - will start a local server on at `http://localhost:8282/` and watch for changes. Uses livereload to refresh browser with each update.

`http://localhost:8282/dist/` - application

`http://localhost:8282/node_modules/intern/client.html?config=tests/intern` - test suites

`grunt build` - build the application and output to a `release` folder.

`grunt e2e` - runs all tests using local [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/).


### Still a beta
* Considering implementing a [widgetloader](https://github.com/odoe/esri-widgetloader)
* Needs ability to inject code into [Application.js](generators/app/templates/src/app/templates/Appication.js)
* Guide on application architecture

### Notes
Uses [theintern.io](https://theintern.github.io/) for testing.

It is recommended that you use NPM 3.x to install dependencies, as this [will reduce the time it takes for Babel to transpile ES2015 code](https://phabricator.babeljs.io/T6756#67810).

### Getting To Know Yeoman

Yeoman has a heart of gold. He's a person with feelings and opinions, but he's very easy to work with. If you think he's too opinionated, he can be easily convinced.

If you'd like to get to know Yeoman better and meet some of his friends, [Grunt](http://gruntjs.com) and [Bower](http://bower.io), check out the complete [Getting Started Guide](https://github.com/yeoman/yeoman/wiki/Getting-Started).


## License

MIT
