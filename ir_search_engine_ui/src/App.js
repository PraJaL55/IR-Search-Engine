import React from 'react';
import { Provider } from 'react-redux';
import { SearchStore } from './store/SearchStore';
import './App.css';
import SearchContainer from './containers/SearchContainer';

const App = () => (
  <div>
    <Provider store={SearchStore}>
      <SearchContainer/>
    </Provider>
  </div>
)

export default App;
