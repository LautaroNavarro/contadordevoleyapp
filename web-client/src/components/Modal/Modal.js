import React, {PureComponent} from 'react';
import './Modal.css';

class Modal extends PureComponent {

    render () {
        return (
          <div className='customModal'>
            <div className='modalContent'>
              <span className='close' onClick={()=>this.props.handleClickClose()}>&times;</span>
              {this.props.children}
            </div>
          </div>
        );
    }
}

export default Modal;
