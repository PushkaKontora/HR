import {BlueButton} from '../../../../styled/buttons/blue-button';
import {InputData} from '../../../../forms/types/form-input-props';
import {ProfileBlock, ProfileBlockProps} from '../../profile-block';

type ProfileDeleteProps = {
  onDelete: () => void;
}

export function ProfileDelete(props: ProfileDeleteProps) {
  const input: ProfileBlockProps = {
    title: 'Удалить аккаунт',
    description: 'Удаление аккаунта является необратимой операцией. Вся информация, связанная с учетной записью, будет полностью удалена.',
    children: (
      <div>
        <BlueButton as={'button'} onClick={props.onDelete}>
          Удалить в любом случае
        </BlueButton>
      </div>
    )
  };

  return (
    <ProfileBlock
      {...input}>
      {input.children}
    </ProfileBlock>
  );
}
