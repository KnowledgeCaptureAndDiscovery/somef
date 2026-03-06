# Reference implementation of the cslEdit library for searching and editing .csl (Citation Style Language) files

This web application allows users of CSL based reference managers to search for citation styles and edit them. It's still an alpha version, but the Visual Editor supports all the features of independent CSL styles (AFAIK) and it should be possible to do real work with it.

It is an implementation of the [CSL editor library](https://github.com/citation-style-editor/csl-editor).

Play with it here: [Citation Style Editor](http://editor.citationstyles.org)

## Prerequisites

- bash (on Windows, I recommend git bash included with [msysgit](http://code.google.com/p/msysgit/downloads/list))
- git
- [Jekyll](https://github.com/mojombo/jekyll/wiki/install)
- Node.js 0.8.4 or later
- Java runtime (optional - for running trang to convert the CSL schema)
- Mail server (for sending feedback emails)

## To Setup Development Version

- Run `git clone --recursive https://github.com/citation-style-editor/csl-editor-demo-site.git csl-demo` to checkout the repo.

- In the repo directory, run `jekyll serve` (optional: add `--watch` to automatically rebuild when source changes).

- Point your browser to `localhost:5001` to view the site locally.

- Point your browser to `localhost:5001/cslEditorLib/pages/unitTests.html` to run the unit tests

## To Deploy

This process creates a static HTML site with concatenated javascript files and cache busters on the URLs, and optionally pushes to the `gh-pages` branch, currently served by github at [http://editor.citationstyles.org](http://editor.citationstyles.org).

- Run `git clone --recursive https://github.com/citation-style-editor/csl-editor-demo-site.git csl-demo` to checkout the repo.

- From the repo directory, run `./deploy.sh $BUILD_DIR $GH_PAGES_REPO_DIR`, where:
  - `$BUILD_DIR` is the name of the directory you wish to deploy to, relative to the parent of the current directory. **All current contents of** `$BUILD_DIR` **will be removed!**
  - `$GH_PAGES_REPO_DIR` (optional) is the name of a checked out `csl-editor-demo-site` repo directory, again relative to the parent of the current directory, which will be used to copy the built version and push the result to the `gh-pages` branch in github, which will automatically update the site at [editor.citationstyles.org](http://editor.citationstyles.org), the domain given in the CNAME file.

- Point your browser to `http://editor.citationstyles.org/cslEditorLib/pages/unitTests.html` to run the unit tests

- Point your browser to `http://editor.citationstyles.org` to view the deployed site

## Customising the editor to integrate with your website or application

Create a fork of this `csl-editor-demo-site` repository and feel free to alter everything for your own needs _except_ for the core library within the `cslEditorLib` git submodule.

Customisable features include:

- Load/Save functions, see `src/visualEditorPage.js`
- Navigation bar and feedback widget, see `html/navigation.html`

You can override these without touching `cslEditorLib`.

## Customising the core library

See documentation for the core library code and it's API at the [CSLEditorLib wiki](https://github.com/citation-style-editor/csl-editor/wiki).

If you fix bugs or otherwise improve the core [cslEditorLib](https://github.com/citation-style-editor/csl-editor) library, ensure the changes are not specific to your implementation and please issue a [pull request](https://github.com/citation-style-editor/csl-editor/pulls) so that everyone can benefit. Thanks!
