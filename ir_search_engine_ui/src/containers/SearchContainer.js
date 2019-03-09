import { connect } from 'react-redux';
import * as SearchActions from '../actions/SearchActions';
import Search from '../components/Search';
import { bindActionCreators } from 'redux';


const mapStateToProps = state => {
    return {
        search: state.search,
        isSearching: state.isSearching,
    };
}

const mapDispatchToProps = dispatch => {
    return bindActionCreators(SearchActions, dispatch);
}

const SearchContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(Search);

export default SearchContainer;