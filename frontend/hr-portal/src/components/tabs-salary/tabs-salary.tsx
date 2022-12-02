import moneyIcon from '../../assets/img/vacancy-card/money.svg';
import moneyRUSIcon from '../../assets/img/job-seach/₽.svg';

type TabsSalaryProps = {
  salary_to?: number,
  salary_from?: number
};

function TabsSalary(props: TabsSalaryProps) {
  const {salary_to, salary_from} = props;
  return (
    <>
      {(salary_to || salary_from) ? (
        <div className="tabsItem">
          <div className="tabs-image">
            <img src={moneyIcon} alt="experience icon"/>
          </div>
          {
            (salary_to !== 0 && salary_from === 0) &&
            (
              <>
                <div className="tabs-text">до {salary_to}</div>
                <div className="tabs-image-rus">
                  <img src={moneyRUSIcon} alt="money rus icon"/>
                </div>
              </>
            )
          }
          {
            salary_to === 0 && salary_from !== 0 &&
            (
              <>
                <div className="tabs-text">от {salary_from}</div>
                <div className="tabs-image-rus">
                  <img src={moneyRUSIcon} alt="money rus icon"/>
                </div>
              </>
            )
          }
          {
            salary_to !== 0 && salary_from !== 0 &&
            (
              <>
                <div className="tabs-text">
                  <div className="tabs-flex">
                    <div className="text">от {salary_from}</div>
                    <div className="tabs-image-rus">
                      <img src={moneyRUSIcon} alt="money rus icon"/>
                    </div>
                  </div>
                  <div className="tabs-flex">
                    <div className="text">до {salary_to}</div>
                    <div className="tabs-image-rus">
                      <img src={moneyRUSIcon} alt="money rus icon"/>
                    </div>
                  </div>
                </div>
              </>
            )
          }
        </div>
      ) : null
      }
    </>
  );
}

export default TabsSalary;