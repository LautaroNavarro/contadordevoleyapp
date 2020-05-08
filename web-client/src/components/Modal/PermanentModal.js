import React, {PureComponent} from 'react';
import './Modal.css';

class PermanentModal extends PureComponent {

    render () {
        return (
          <div className='customModal rounded-lg'>
            <div className='modalContent bg-light'>
              {this.props.children}
            </div>
          </div>
        );
    }
}

export default PermanentModal;