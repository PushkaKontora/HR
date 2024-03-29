import likesIcon from '../../assets/img/vacancy-card/no_like.svg';
import './resume-card.scss';
import {ResumeUser} from '../../types/resume';
import experienceIcon from '../../assets/img/vacancy-card/experience.svg';
import moneyIcon from '../../assets/img/vacancy-card/money.svg';
import placeholder from '../../assets/svg/placeholder.svg';
import {extractFileNameFromYandex, getExperienceOptionByKey} from '../../utils/resume';
import {Icon, UserIcon, ResumeField, Contacts, CompetencyItem} from './styled';
import {ResumeTitle} from '../styled/resume/resume-title';
import {LoadButton} from '../../reused-components/load-button/load-button';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {useEffect, useState} from 'react';
import {isFavorite} from '../../utils/favorite';
import {addToVacancyWishlist, deleteFromVacancyWishlist} from '../../service/async-actions/async-actions-vacancy';
import {toast} from 'react-toastify';
import {
  addToResumeWishlist,
  deleteToResumeWishlist,
  getResumeWishlist, ResumeWishListSortBy
} from '../../service/async-actions/async-actions-resume';
import {LikeButton} from '../../reused-components/like-button/like-button';
import copyIcon from '../../assets/icons/copy.svg';

type VacancyCard = {
  resume: ResumeUser
}

function ResumeCard({resume}: VacancyCard) {
  const handleClickVacancyCard = () => {
    //dispatch(setVacancyByID(vacancy));
    //navigate(`${NoAuthRoutes.Vacancy}/${vacancy.id}`);
  };

  const dispatch = useAppDispatch();
  const favoriteResumes = useAppSelector((state) => state.user.favoriteResumes);

  const [liked, setLiked] = useState(isFavorite(resume, favoriteResumes));
  const [showContacts, setShowContacts] = useState(false);

  useEffect(() => {
    let mounted = true;

    if (mounted) {
      setLiked(isFavorite(resume, favoriteResumes));
    }

    return () => {
      mounted = false;
    };
  }, [favoriteResumes]);

  const like = () => {
    if (resume) {
      dispatch(addToResumeWishlist(resume.id))
        .then(() => {
          toast.success('Резюме добавлено в избранное');
          setLiked(true);
          dispatch(getResumeWishlist(ResumeWishListSortBy.added_at_desc));
        });
    }
  };

  const dislike = () => {
    if (resume) {
      dispatch(deleteToResumeWishlist(resume.id))
        .then(() => {
          toast.error('Резюме удалено из избранного');
          setLiked(false);
          dispatch(getResumeWishlist(ResumeWishListSortBy.added_at_desc));
        });
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success('Скопировано');
  };

  return (
    <div className="resumeCardWrapper" onClick={handleClickVacancyCard}>
      <div className='resumeCardBg'>
        <div className="resumeCardItem resumeCardItem__content">
          <div className="resumeCardInfo resumeCardInfo__title">
            {resume.desired_job}
          </div>
          <div className="resumeCardInfo resumeCardInfo__description">
            {
              resume.experience &&
                <ResumeField>
                  <Icon src={experienceIcon}/>
                  {getExperienceOptionByKey(resume.experience)}
                </ResumeField>
            }
            {
              resume.desired_salary !== 0 &&
                <ResumeField>
                  <Icon src={moneyIcon}/>
                  {resume.desired_salary} ₽
                </ResumeField>
            }
          </div>
          <div className="resumeCardInfo resumeCardInfo__tabs">
            {resume.competencies.map((item, idx) => {
              return (
                <div key={idx} className="tabsItem">
                  {item}
                </div>);
            })}
          </div>
        </div>
        <UserIcon src={resume.owner.photo || placeholder}/>
      </div>
      <div className="resumeCardItem resumeCardItem__action">
        <div className='resumeDownload'>
          <ResumeTitle bgColor={'#fff'}>
            {extractFileNameFromYandex(resume.document)}
          </ResumeTitle>
          <a href={resume?.document} download>
            <LoadButton bgColor={'#fff'} onClick={() => {return;}}/>
          </a>
        </div>

        <div className="actionItem navTabs">
          <LikeButton
            onLike={like}
            onDislike={dislike}
            liked={liked}/>
          <button
            className="navTabs-btnItem navTabs-btnItem__respond"
            onClick={() => setShowContacts(!showContacts)}
          >
            {showContacts ? 'Скрыть контакты' : 'Показать контакты'}
          </button>
          {
            showContacts &&
              <Contacts onClick={() => copyToClipboard(resume?.owner.email)}>
                {resume?.owner.email}
                <img style={{marginLeft: '10px'}} src={copyIcon} alt={'копир.'}/>
              </Contacts>
          }
        </div>
      </div>
    </div>
  );
}

export default ResumeCard;
