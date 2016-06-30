import React, { Component } from 'react';
import FocusManager from './FocusManager';
import debounce from './debounce';
import {findDOMNode} from 'react-dom';

class SearchBox extends Component {
  render() {
    let {onChange, onBlur, onFocus} = this.props;
    onFocus = onFocus.bind(this, 'searchbox');
    onBlur = onBlur.bind(this, 'searchbox');
    return (
      <input type="search" value={this.props.query} ref="searchbox" {...{onChange, onBlur, onFocus}} placeholder="search..."/>
    )
  }
}

class SearchControls extends Component {
  render() {
    let {onFocus, onBlur, waiting, totalCount, from, count, getNext, getPrev} = this.props
    if (!count) {
      return null;
    }
    return (
      <div onMouseDown={onFocus.bind(this, 'searchControls')}
           onMouseUp={onBlur.bind(this, 'searchControls')}
           onTouchStart={onBlur.bind(this, 'searchControls')}
           onTouchEnd={onBlur.bind(this, 'searchControls')}
           >
        <div >
          {from} to {from + count} of {totalCount} results
        </div>
        <button onFocus={onFocus.bind(this, 'btn-prev')}
                onBlur={onBlur.bind(this, 'btn-prev')}
                onClick={onFocus.bind(this, 'btn-prev')}
                disabled={from <= 0}
                onClick={getPrev}>
          &lt; previous
        </button>
        <button onFocus={onFocus.bind(this, 'btn-next')} 
                onBlur={onBlur.bind(this, 'btn-next')}
                onClick={onFocus.bind(this, 'btn-next')}
                disabled={totalCount <= (from + count)}
                onClick={getNext}>
          next &gt;
        </button>
      </div>)
  }
}

class SearchResult extends Component {
  render() {
    let {onFocus, onBlur, Key, title, body} = this.props;
    onFocus = onFocus.bind(this, Key);
    onBlur = onBlur.bind(this, Key);
    return (
      <a href={this.props.url} tabIndex="0" {...{onFocus, onBlur}}>
        <div className='result'>
          <h1 dangerouslySetInnerHTML={{__html: title}} />
          <p dangerouslySetInnerHTML={{__html: body}} />
        </div>
      </a>
    )
  }
}

class SearchResults extends Component {
  render() {
    let {results, onFocus, onBlur, waiting, totalCount, from, getNext, getPrev} = this.props;

    let content = (<p>no results</p>)

    if (results.length) {
      content = results.map((result, i) => {
        return (<SearchResult {...result} key={'result-'+i} {...{onFocus, onBlur}} />)
      })
    } else if (waiting) {
      content = (<p>searching...</p>)
    }
    return (
      <div className='results'>
        {content}
        <SearchControls {...{waiting, totalCount, from, onFocus, onBlur, getNext, getPrev}} count={results.length} />
      </div>
    );
  }
}

export default class Search extends FocusManager {
  constructor(props) {
    super(props);
    this.state = {...this.state, query: '', from: 0, results: [], waiting: 0, totalCount: 0};
    this._makeSearch = debounce(this.__makeSearch, 150)
  }

  render() {
    let {results, waiting, query, from, totalCount, focused} = this.state;
    let onFocus = this.handleFocus;
    let onBlur = this.handleBlur;
    let getNext = this.nextResults;
    let getPrev = this.prevResults;
    var searchResults = null;
    if (focused && (query.length >= this.props.minSearchLength)) {
      searchResults = <SearchResults {...{results, waiting, totalCount, from, onFocus, onBlur, getNext, getPrev}} />;
    }
    return (
      <div>
        <SearchBox onChange={this.handleQueryChange} {...{query, onFocus, onBlur}} ref="searchInput" />
        {searchResults}
      </div>
    );
  }

  handleQueryChange = (event) => {
    var query = event.target.value;
    this.setState({query: query, from: 0});
    this.makeSearch(query);
  }

  nextResults = () => {
    let from = this.state.from + 5;
    this.makeSearch(this.state.query, from);
  }

  prevResults = () => {
    let from = Math.max(this.state.from - 5, 0);
    this.makeSearch(this.state.query, from);
  }

  makeSearch = (query, from) => {
    if (query.length >= this.props.minSearchLength) {
      this._makeSearch(query, from);
    }    
  }

  __makeSearch = (query, from) => {
    from = from || 0;
    var xhr = new XMLHttpRequest();
    this.setState({waiting: this.state.waiting + 1});
    xhr.open('POST', window.searchHost + window.queryUrl);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = this.handleSearchResponse;
    xhr.from = from;
    xhr.send(JSON.stringify({
        "file": "search", 
        "params": {
            "query_string": query,
            "from": from,
        },
    }));
  }

  handleSearchResponse = (event) => {
    let xhr = event.target;

    let newState = {waiting: Math.max(this.state.waiting - 1, 0)}
    if (xhr.status === 200) {
      let results = JSON.parse(xhr.responseText).hits || {};
      newState.totalCount = results.total || 0;
      results = results.hits || [];
      newState.from = xhr.from;
      newState.results = results.map(function(result) { return {title: (result.highlight.title || [result._source.title])[0], body: result.highlight.body[0], url: result._source.url}});
    }
    this.setState(newState);

    let searchInput = findDOMNode(this.refs.searchInput);
    if (document.activeElement != searchInput) {
      searchInput.focus();
    }
  }
}

Search.defaultProps = {minSearchLength: 3}
