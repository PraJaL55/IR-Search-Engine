import * as configConstants from '../config/config';

export const RECEIVE_SEARCH = "RECEIVE_SEARCH";
export const RECEIVE_IS_SEARCHING = "RECEIVE_IS_SEARCHING";

export function receiveIsSearching(isSearching){
    return { 
        type: RECEIVE_IS_SEARCHING, 
        isSearching 
    };
}  


function receiveSearch(search){
    return { 
        type: RECEIVE_SEARCH, 
        search 
    };
} 


export function requestSearch(searchQuery){
    return async (dispatch) => {
        try{
            const response = await fetch(configConstants.fetchSearchUrl,
                {  
                    method: 'POST',
                    body: searchQuery
                }
            );
            let json = await response.json();
            dispatch(receiveIsSearching(false));
            return dispatch(receiveSearch(json));
        } 
        catch(error)
        {
            console.log(searchQuery)
            console.error('Error fetching search-results', error);
        }
    }
}

