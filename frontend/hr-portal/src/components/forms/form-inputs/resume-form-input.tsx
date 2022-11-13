import { FormInputProps } from '../types/form-input-props';
import {XLargeRegular} from '../../styled/fonts/x-large';
import AbstractFormInput from './abstract-form-input';
import {LargeLight} from '../../styled/fonts/large';

function ResumeFormInput(props: FormInputProps) {
  return (
    <AbstractFormInput
      normalBorderColor={'#000'}
      padding={'16px'}
      inputMarginBottom={'16px'}
      fontComponent={LargeLight}
      inputRef={props.inputRef}
      {...props}/>
  );
}

export default ResumeFormInput;
