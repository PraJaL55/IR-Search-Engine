import { createStore, applyMiddleware } from 'redux';
import { searchReducer } from '../reducers/SearchReducer';
import thunkMiddleware from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension';

export const SearchStore = createStore(searchReducer,
    composeWithDevTools(applyMiddleware(
        thunkMiddleware // lets us dispatch() functions
    )));