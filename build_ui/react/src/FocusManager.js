import React, { Component } from 'react';

export default class FocusManager extends Component {
  constructor(props) {
    super(props);
    this.state = {focused: false, mouseDown: false, touch: false};
  }

  isFocused = (state) => {
    state = state || this.state;
    return state.focused || state.mouseDown || state.touch;
  }

  handleFocus = (e) => this.setFocusComponent({focused: true}, 'focus')
  handleBlur = (e) => setTimeout(this.setFocusComponent, 100, {focused: false}, 'blur')

  handleMouseDown = (e) => this.setFocusComponent({mouseDown: true}, 'mouseDown')
  handleMouseUp = (e) => setTimeout(this.setFocusComponent, 100, {mouseDown: false}, 'mouseUp')

  handleTouchStart = (e) => this.setFocusComponent({touch: true}, 'touchStart')
  handlTouchEnd = (e) => setTimeout(this.setFocusComponent, 100, {touch: false}, 'touchEnd')

  setFocusComponent = (newState, e) => {
    let wasFocused = this.isFocused();
    newState = {...this.state, ...newState};
    this.setState(newState);
    let isFocused = this.isFocused(newState);
    if (wasFocused != isFocused) {
      if (isFocused) {
        this.props.onFocus(e);
      } else {
        this.props.onBlur(e);
      }
    }
  }

  render = () => {
    let handlers = {onFocus: this.handleFocus, onBlur: this.handleBlur, onMouseDown: this.handleMouseDown, onMouseUp: this.handleMouseUp, onTouchStart: this.handleTouchStart, onTouchEnd: this.handlTouchEnd};
    return (
      <div {...this.props} {...handlers}>
        {this.props.children}
      </div>
    )
  }

}


