import LoginForm from '../../components/forms/login-form/login-form';
import {Title} from '../../components/styled/forms/title';
import {BackgroundImage, ParentForBackgroundImage} from '../../components/styled/forms/background-image';
import {LargeRegular} from '../../components/styled/fonts/large';
import {BlueLink} from '../../components/styled/links/blue';
import {NoAuthRoutes} from '../../const/app-routes';
import {Content} from '../../components/styled/markup/content';

function LoginPage() {
  return (
    <Content>
      <Title marginTop={'160px'}>Войдите в свой профиль</Title>
      <LoginForm/>
      <ParentForBackgroundImage>
        <BackgroundImage/>
      </ParentForBackgroundImage>

      <LargeRegular style={{marginBottom: '160px'}}>
        <BlueLink to={''}>Забыли пароль?</BlueLink>
        <p style={{marginTop: '16px'}}>
          Нет аккаунта? <BlueLink to={NoAuthRoutes.SignUp}>Зарегистрироваться сейчас.</BlueLink>
        </p>
      </LargeRegular>
    </Content>
  );
}

export default LoginPage;
