import {Button, Icon} from './styled/styles';
import bg from '../assets/icons/upload.svg';

type LoadButtonProps = {
  onClick: () => void;
}

export function LoadButton({onClick}: LoadButtonProps) {
  return (
    <Button onClick={onClick} type={'button'}>
      <Icon src={bg}/>
    </Button>
  );
}