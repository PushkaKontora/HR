import AuthFormInput from '../form-inputs/auth-form-input';
import {InputData} from '../types/form-input-props';
import {useState} from 'react';
import {useForm} from 'react-hook-form';
import {FormSubmit} from '../../styled/forms/form-submit';
import {EmailRegex} from '../../../const/email-regex';
import {useAppDispatch} from '../../../app/hooks';
import {signIn} from '../../../service/async-actions';
import {SignInData} from '../../../types/sign-in-data';

function SignUpForm() {
  const {
    register,
    handleSubmit,
    formState: {errors}
  } = useForm<SignInData>({
    mode: 'onChange'
  });

  const dispatch = useAppDispatch();

  const [formData, setFormData] = useState({
    surname: '',
    name: '',
    patronymic: '',
    email: '',
    password: ''
  });

  const inputs: InputData[] = [
    {
      name: 'surname',
      label: 'Фамилия',
      type: 'text',
      options: {
        required: 'Вы не ввели свою фамилию'
      }
    },
    {
      name: 'name',
      label: 'Имя',
      type: 'text',
      options: {
        required: 'Вы не ввели свое имя'
      }
    },
    {
      name: 'patronymic',
      label: 'Отчество',
      type: 'text',
      options: {
      }
    },
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
        required: 'Вы не ввели пароль',
        minLength: {
          value: 8,
          message: 'Пароль должен содержать не менее 8 символов'
        }
      }
    }
  ];

  const onSubmit = (data: SignInData) => {
    dispatch(signIn(data));
  };

  return (
    <form action={'#'} onSubmit={handleSubmit(onSubmit)}>
      {inputs.map((item, idx) => (
        <AuthFormInput key={idx} {...item} errors={errors} register={register}/>
      ))}

      <FormSubmit type='submit' value='Далее'/>
    </form>
  );
}

export default SignUpForm;
