import {Vacancy} from '../../types/vacancy';
import experienceIcon from '../../assets/img/vacancy-card/experience.svg';
import './vacancy-card.scss';
import {ExpectedExperienceNameString} from '../../const';
import {useAppDispatch} from '../../app/hooks';
import {setVacancyByID} from '../../features/vacancy/vacancy-slice';
import {useNavigate} from 'react-router-dom';
import ButtonActionVacancyCard from '../button-action-vacancy-card/button-action-vacancy-card';
import UseEditor from '../../reused-components/text-editor/useEditor';
import {useEffect, useState} from 'react';
import TabsSalary from '../tabs-salary/tabs-salary';

type VacancyCardProps = {
  vacancy: Vacancy
}

function VacancyCard(props: VacancyCardProps) {
  const {vacancy} = props;
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const [convertedContent, setConvertedContent] = useState('');

  const vacancyExperience = ExpectedExperienceNameString[vacancy.expected_experience as keyof typeof ExpectedExperienceNameString];
  const handleClickVacancyCard = () => {
    dispatch(setVacancyByID(vacancy));
    navigate(`/${vacancy.id}`);
  };

  const createMarkup = (html: any) => {
    return UseEditor(html).fromHtml();
  };

  useEffect(() => {
    if (vacancy.description) {
      setConvertedContent(vacancy.description);
    } else {
      setConvertedContent('<p></p>');
    }
  }, [vacancy]);

  return (
    <div className="vacancyCardWrapper" onClick={handleClickVacancyCard}>
      <div className="vacancyCardItem vacancyCardItem__content">
        <div className="vacancyCardInfo vacancyCardInfo__title">
          {vacancy.name}
        </div>
        <div
          className="vacancyCardInfo vacancyCardInfo__description"
          dangerouslySetInnerHTML={createMarkup(convertedContent)}
        />
        <div className="vacancyCardInfo vacancyCardInfo__tabs">
          <div className="tabsItem">
            <div className="tabs-image">
              <img src={experienceIcon} alt="money icon"/>
            </div>
            <div className="tabs-text">
              {vacancyExperience}
            </div>
          </div>
          <TabsSalary salary_to={vacancy?.salary_to} salary_from={vacancy?.salary_from}/>
        </div>
      </div>
      <div className="vacancyCardItem vacancyCardItem__action">
        <div className="actionItem actionItem__department">
          <span>{vacancy.department.name}</span> {vacancy.department.leader.name} {vacancy.department.leader.surname}
        </div>
        <div className="actionItem navTabs">
          <ButtonActionVacancyCard vacancy={vacancy}/>
        </div>
      </div>
    </div>
  );
}

export default VacancyCard;

//TODO: сделать лайк закрашенным, если выбран в избранное у пользователя