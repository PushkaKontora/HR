import AuthFormInput from '../form-inputs/auth-form-input';
import {InputData} from '../types/form-input-props';
import {useEffect, useState} from 'react';
import {useForm} from 'react-hook-form';
import {FormSubmit} from '../../styled/forms/form-submit';
import {EmailRegex} from '../../../const/email-regex';
import {useAppDispatch, useAppSelector} from '../../../app/hooks';
import {signUp} from '../../../service/async-actions/async-actions-user';
import {SignInData} from '../../../types/sign-in-data';
import {EMAIL_OPTIONS, PASSWORD_OPTIONS} from '../../../const/forms/input-options';
import {UserStatus} from '../../../types/user-status';
import {redirect, useLocation, useNavigate} from 'react-router-dom';
import {AuthRoutes} from '../../../const/app-routes';

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
    emailRoute: '',
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
        ...EMAIL_OPTIONS
      }
    },
    {
      name: 'password',
      label: 'Пароль',
      type: 'password',
      options: {
        required: 'Вы не ввели пароль',
        ...PASSWORD_OPTIONS
      }
    }
  ];

  const userStatus = useAppSelector((state) => state.general.statusUser);
  const navigate = useNavigate();

  useEffect(() => {
    let mounted = true;

    if (mounted) {
      if (userStatus !== UserStatus.noAuth) {        if (userStatus === UserStatus.user) {
          navigate(AuthRoutes.Vacancies);
        }
        else if (userStatus === UserStatus.employer) {
          navigate(AuthRoutes.Vacancies);
        }
      }
    }

    return () => {
      mounted = false;
    };
  }, [userStatus]);

  const onSubmit = (data: SignInData) => {
    dispatch(signUp(data));
    //.then(() => {redirect(location.state.prevLocation);});
    //.then(() => {window.location.reload();});
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
