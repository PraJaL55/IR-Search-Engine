import * as SearchActions from '../actions/SearchActions';

const initialState = {
    search: {
        'www.google.com': ['Google', 'this is home for google'],
        'www.facebook.com': ['Facebook Inc', 'this is home for facebook']
    },
    isSearching: false
};

export function searchReducer(state = initialState, action){
    switch(action.type) {
        case SearchActions.RECEIVE_SEARCH:
            return {
                ...state,
                products: action.searchResult,
            };
        case SearchActions.RECEIVE_IS_SEARCHING:
            return {
                ...state,
                isSearching: action.isSearching,
            };
        default:
            return state;
    }
}