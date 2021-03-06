import React, { Component } from 'react';
import axios from 'axios';
import { NavLink, Route, Switch, withRouter } from 'react-router-dom';

import Album from './Album';
import config from '../config';


class Photos extends Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      photoshoots: [],
      photos: [],
    }
  }
  
  componentDidMount() {
    axios.get(config.photosEndpoint)
    .then(response => this.setState({ photoshoots: response.data, isLoaded: true }))
    .catch(error => this.setState({ error, isLoaded: true }));
  }

  render() {
    const { error, isLoaded, photoshoots, photos } = this.state;
    if (error) {
      return <div className="div-padding">Error: {error.message}</div>
    } else if (!isLoaded) {
      return <div className="div-padding">Looking...</div>
    }

    const albumDateArray = photoshoots.data.map((item, i) =>
      <NavLink
        key={`${i}-${item}`}
        className="photoshoot-album link"
        activeClassName="active-photoalbum-item"
        to={`${this.props.match.path}/${item}`}
      >
        {item}
      </NavLink>
    );

    const switchArray = photoshoots.data.map((item, i) =>
      <Route
        key={`${i}-switch-${item}`}
        path={`${this.props.match.path}/${item}`}
        component={() => <Album photoshootDate={item} />}
      />
    );

    return (
      <div>
        <Switch>
          {switchArray}
        </Switch>
        <div className="photoshoot-nav">
          {albumDateArray}
        </div>
      </div>
    );
  }
}

export default withRouter(Photos);
