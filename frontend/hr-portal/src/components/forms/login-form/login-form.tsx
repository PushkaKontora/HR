import './login-form.scss';
import {useForm} from 'react-hook-form';
import {useState} from 'react';
import FormInput from '../form-input/form-input';
import {InputData} from '../types/form-input-props';
import {FormSubmit} from '../../styled/forms/form-submit';
import {EmailRegex} from '../../../const/email-regex';

type LoginFormData = {
  email: string
  password: string
}

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: {errors}
  } = useForm<LoginFormData>({
    mode: 'onChange'
  });

  // useState будет переписан на Redux
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const inputs: InputData[] = [
    {
      name: 'email',
      label: 'Email',
      type: 'email',
      options: {
        required: 'Вы не ввели e-mail',
        pattern: {
          value: EmailRegex,
          message: 'Введите корректный e-mail'
        }
      }
    },
    {
      name: 'password',
      label: 'Пароль',
      type: 'password',
      options: {
        required: 'Вы не ввели пароль'
      }
    }
  ];

  const onSubmit = (data: LoginFormData) => {
    setFormData({...data});
  };

  return (
    <form action={'#'} onSubmit={handleSubmit(onSubmit)}>
      {inputs.map((item, idx) => (
        <FormInput key={idx} {...item} errors={errors} register={register}/>
      ))}

      <FormSubmit type='submit' value='Далее'/>
    </form>
  );
}

export default LoginForm;
