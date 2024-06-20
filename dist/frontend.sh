#!/bin/bash

PROJECT_PATH=$(pwd ${BASH_SOURCE[0]}/../)
BOOTSTRAP_PATH=${PROJECT_PATH}/node_modules/bootstrap
FONTAWESOME_PATH=${PROJECT_PATH}/node_modules/@fortawesome/fontawesome-free
THEME_AGENCY_PATH=${PROJECT_PATH}/node_modules/startbootstrap-agency

build_boostrap() {
  echo ">>> Copy bootstrap"
  rm -Rf $PROJECT_PATH/portfolio/static/bootstrap
  cp -Ra $BOOTSTRAP_PATH/dist $PROJECT_PATH/portfolio/static/bootstrap
}

build_fontawesome() {
  echo ">>> Copy fontawesome"
  rm -Rf $PROJECT_PATH/portfolio/static/fontawesome
  mkdir $PROJECT_PATH/portfolio/static/fontawesome
  cp -Ra $FONTAWESOME_PATH/{js,css} $PROJECT_PATH/portfolio/static/fontawesome/
}

build_agency() {
  echo ">>> Override SCSS variables"
  cp $PROJECT_PATH/dist/scss/_colors.scss $THEME_AGENCY_PATH/src/scss/variables/

  echo ">>> Build Agency Theme"
  cd $THEME_AGENCY_PATH && npm install && npm run build
  rm -Rf $PROJECT_PATH/portfolio/static/agency
  cp -Ra $THEME_AGENCY_PATH/dist $PROJECT_PATH/portfolio/static/agency
  rm -f $PROJECT_PATH/portfolio/static/agency/index.html
}

build_boostrap
build_fontawesome
build_agency
