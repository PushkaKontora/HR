import SignUpForm from '../../components/forms/sign-up-form/sign-up-form';
import {BackgroundImage, ParentForBackgroundImage} from '../../components/styled/forms/background-image';
import {Title} from '../../components/styled/forms/title';
import {BlueLink} from '../../components/styled/links/blue';
import {LargeRegular} from '../../components/styled/fonts/large';
import {NoAuthRoutes} from '../../const/app-routes';

function SignUpPage() {
  return (
    <div>
      <Title marginTop={'0'}>Создайте свой профиль</Title>
      <SignUpForm/>
      <ParentForBackgroundImage>
        <BackgroundImage/>
      </ParentForBackgroundImage>

      <LargeRegular>
        <p>
          Уже есть аккаунт? <BlueLink to={NoAuthRoutes.Login}>Войти</BlueLink>
        </p>
      </LargeRegular>
    </div>
  );
}

export default SignUpPage;
