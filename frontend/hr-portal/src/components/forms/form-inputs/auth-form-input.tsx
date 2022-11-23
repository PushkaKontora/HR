import { FormInputProps } from '../types/form-input-props';
import AbstractFormInput from './abstract-form-input';
import {XLargeRegular} from '../../styled/fonts/x-large';

function AuthFormInput(props: FormInputProps) {
  return (
    <AbstractFormInput
      width={'525px'}
      normalBorderColor={'#9C9C9C'}
      borderWidth={'1px'}
      padding={'20px'}
      inputMarginBottom={'32px'}
      fontComponent={XLargeRegular}
      {...props}/>
  );
}

export default AuthFormInput;
