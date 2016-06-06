import React, { Component } from 'react';

function _hasFocus(focii) {
  var k, v;
  for (k in focii) {
    v = focii[k];
    if (v) {return true;}
  }
  return false;
}

export default class FocusManager extends Component {
  constructor(props) {
    super(props);
    this.state = {focii: {}, focused: false};
  }

  handleFocus = (key) => {
    this._updateFocii(key, true);
  }

  handleBlur = (key) => {
    setTimeout(this._updateFocii, 100, key, false);
  }

  _updateFocii = (key, isFocused) => {
    let focii = {...this.state.focii};
    focii[key] = isFocused;
    this.setState({focii: focii, focused: _hasFocus(focii)});
  }
}
