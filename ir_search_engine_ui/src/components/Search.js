import React, { Component } from 'react';
import Paper from '@material-ui/core/Paper';
import InputBase from '@material-ui/core/InputBase';
import IconButton from '@material-ui/core/IconButton';
import SearchIcon from '@material-ui/icons/Search';
import CircularProgress from '@material-ui/core/CircularProgress';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';

const styles = {
    searchBoxAnimation: {
        transform: 'translate(-600px, -280px)'
    },
    root: {
        padding: '2px 4px',
        display: 'flex',
        alignItems: 'center',
        width: '33%',
        position: 'fixed',
        borderRadius: '25px',
        top: '33%',
        left: '33%',
      },
      input: {
        marginLeft: 15,
        flex: 1,
      },
      iconButton: {
        padding: 10,
      },
      circularProgress: {
        position: 'fixed',
        top: '50%',
        left: '50%',
        color: '#00695C',
    },
    searchBox:{
        position: 'fixed',
        top: '12%',
        paddingLeft: '2%',
        paddingRight: '2%',
        width: '80%'
    },
    searchInfo: {
        marginTop: '20px'
    },
    title: {
        padding: '5px',
    },
    link: {
        textDecoration: 'none',
        color: '#c00',

        '&:hover': {
            color: '#ff4f30' 
        }
    },
    snippet: {
        padding: '5px',
        color: '#303030'
    }
};

class Search extends Component {
    constructor(props) {
        super(props);
        this.searchResult = this.searchResult.bind(this);
    }

    searchResult() {
        this.props.receiveIsSearching(true);
    }
    
    render(){
        return(
            <div>
                <Paper className={classNames(this.props.classes.root, {
                                                [this.props.classes.searchBoxAnimation]: this.props.isSearching === true})} elevation={1}>
                    <InputBase className={this.props.classes.input} placeholder="Search ICS" />
                    <IconButton className={this.props.classes.iconButton} aria-label="Search" onClick = {this.searchResult}>
                        <SearchIcon />
                    </IconButton>
                </Paper>
                <div>
                {
                    this.props.isSearching ? <CircularProgress className={this.props.classes.circularProgress} /> : '' 
                }
                </div>
                <div className = {this.props.classes.searchBox}>
                {
                    this.props.search ?
                    
                    Object.entries(this.props.search).map(([url, list], index) => {
                        return(
                        <Paper className={this.props.classes.searchInfo} elevation={1} key = {index} >
                            <Typography variant="h5" component="h4" className= {this.props.classes.title} key = {index}>
                                <a target="_blank" href = {url} className = {this.props.classes.link}>{list[0]}</a> 
                            </Typography>
                            <Typography variant="h6" component="p" className= {this.props.classes.snippet} key={index}>
                               {list[1]}
                            </Typography>
                        </Paper>
                        )
                    })    
                    : ''
                }
                </div>
            </div>
        );
    }
}

export default  withStyles(styles)(Search)