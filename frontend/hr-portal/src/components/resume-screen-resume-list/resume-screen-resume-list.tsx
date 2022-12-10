import {useAppSelector} from '../../app/hooks';
import ResumeCard from '../resume-card/resume-card';
import './resume-screen-resume-list.scss';
import PaginationCustom from '../pagination-custom/paginationCustom';

function ResumeScreenResumeList() {
  const resumeList = useAppSelector((state) => state.resume.resumeList);

  return (
    <div className="contentItem contentItem__vacancies">
      {
        resumeList ? (
          <>
            <div className="cardVacancy-title">
              <div className="title">Найдено {resumeList.count} резюме</div>
            </div>
            {
              resumeList.items.map((item, idx) => {
                return (
                  <ResumeCard key={idx} resume={item}/>
                );
              })
            }
            <PaginationCustom itemList={resumeList.items}/>
          </>
        ) : null
      }
    </div>
  );
}

export default ResumeScreenResumeList;