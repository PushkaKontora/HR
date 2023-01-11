import {Icon} from './styles';
import deleteIcon from '../../assets/icons/delete-rounded.svg';
import {ResumeTitle} from '../../components/styled/resume/resume-title';

type ClickableResumeTitleProps = {
  item: string,
  showDeleteButtons: boolean,
  onDelete?: () => void
};

export function ClickableResumeTitle({item, showDeleteButtons, onDelete}: ClickableResumeTitleProps) {
  return (
    <ResumeTitle style={{marginRight: '8px', height: '42px'}} padding={'12px 15px 12px 24px'}>
      <div>{item}</div>
      {showDeleteButtons && <button style={{backgroundColor: '#0000'}} type={'button'} onClick={() => {
        if (onDelete) onDelete();
      }}>
        <Icon src={deleteIcon}/>
      </button>}
    </ResumeTitle>
  );
}
