import React, { Component } from 'react';
import FocusManager from './FocusManager';
import debounce from './debounce';
import {findDOMNode} from 'react-dom';

class SearchBox extends Component {
  render() {
    let {onChange} = this.props;
    return (
      <input type="search" value={this.props.query} ref="searchbox" {...this.props} placeholder="search the code..."/>
    )
  }
}

class SearchControls extends Component {
  render() {
    let {waiting, totalCount, from, count, getNext, getPrev} = this.props
    if (!count) {
      return null;
    }
    return (
      <div>
        <div >
          {from} to {from + count} of {totalCount} results
        </div>
        <button disabled={from <= 0}
                onClick={getPrev}>
          &lt; previous
        </button>
        <button disabled={totalCount <= (from + count)}
                onClick={getNext}>
          next &gt;
        </button>
      </div>)
  }
}

class SearchResult extends Component {
  render() {
    let {title, body} = this.props;
    return (
      <a href={this.props.url} tabIndex="0">
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
    let {results, waiting, totalCount, from, getNext, getPrev} = this.props;

    let content = (<p>no results</p>)

    if (results.length) {
      content = results.map((result, i) => {
        return (<SearchResult {...result} key={'result-'+i}  />)
      })
    } else if (waiting) {
      content = (<p>searching...</p>)
    }
    return (
      <div className='results'>
        {content}
        <SearchControls {...{waiting, totalCount, from, getNext, getPrev}} count={results.length} />
      </div>
    );
  }
}

export default class Search extends Component {
  constructor(props) {
    super(props);
    this.state = {focused: false, query: '', from: 0, results: [], waiting: 0, totalCount: 0};
    this._makeSearch = debounce(this.__makeSearch, 150)
  }

  render() {
    let {results, waiting, query, from, totalCount, focused} = this.state;
    let getNext = this.nextResults;
    let getPrev = this.prevResults;
    var searchResults = null;
    if (focused && (query.length >= this.props.minSearchLength)) {
      searchResults = <SearchResults {...{results, waiting, totalCount, from, getNext, getPrev}} />;
    }
    return (
      <FocusManager onFocus={this.handleFocus} onBlur={this.handleBlur}>
        <SearchBox onChange={this.handleQueryChange} query={query} ref="searchInput" />
        {searchResults}
      </FocusManager>
    );
  }

  handleFocus = () => this.setState({focused: true});
  handleBlur = (e) => {
    this.setState({focused: false});
    if (e != 'blur') {
      findDOMNode(this.refs.searchInput).focus();
    }
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
  }
}

Search.defaultProps = {minSearchLength: 3}
