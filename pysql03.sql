----https://oracle-base.com/articles/misc/analytic-functions
--DROP TABLE emp PURGE;

CREATE TABLE emp (
  empno    NUMBER(4) CONSTRAINT pk_emp PRIMARY KEY,
  ename    VARCHAR2(10),
  job      VARCHAR2(9),
  mgr      NUMBER(4),
  hiredate DATE,
  sal      NUMBER(7,2),
  comm     NUMBER(7,2),
  deptno   NUMBER(2)
);

INSERT INTO emp VALUES (7369,'SMITH','CLERK',7902,to_date('17-12-1980','dd-mm-yyyy'),800,NULL,20);
INSERT INTO emp VALUES (7499,'ALLEN','SALESMAN',7698,to_date('20-2-1981','dd-mm-yyyy'),1600,300,30);
INSERT INTO emp VALUES (7521,'WARD','SALESMAN',7698,to_date('22-2-1981','dd-mm-yyyy'),1250,500,30);
INSERT INTO emp VALUES (7566,'JONES','MANAGER',7839,to_date('2-4-1981','dd-mm-yyyy'),2975,NULL,20);
INSERT INTO emp VALUES (7654,'MARTIN','SALESMAN',7698,to_date('28-9-1981','dd-mm-yyyy'),1250,1400,30);
INSERT INTO emp VALUES (7698,'BLAKE','MANAGER',7839,to_date('1-5-1981','dd-mm-yyyy'),2850,NULL,30);
INSERT INTO emp VALUES (7782,'CLARK','MANAGER',7839,to_date('9-6-1981','dd-mm-yyyy'),2450,NULL,10);
INSERT INTO emp VALUES (7788,'SCOTT','ANALYST',7566,to_date('13-JUL-87','dd-mm-rr')-85,3000,NULL,20);
INSERT INTO emp VALUES (7839,'KING','PRESIDENT',NULL,to_date('17-11-1981','dd-mm-yyyy'),5000,NULL,10);
INSERT INTO emp VALUES (7844,'TURNER','SALESMAN',7698,to_date('8-9-1981','dd-mm-yyyy'),1500,0,30);
INSERT INTO emp VALUES (7876,'ADAMS','CLERK',7788,to_date('13-JUL-87', 'dd-mm-rr')-51,1100,NULL,20);
INSERT INTO emp VALUES (7900,'JAMES','CLERK',7698,to_date('3-12-1981','dd-mm-yyyy'),950,NULL,30);
INSERT INTO emp VALUES (7902,'FORD','ANALYST',7566,to_date('3-12-1981','dd-mm-yyyy'),3000,NULL,20);
INSERT INTO emp VALUES (7934,'MILLER','CLERK',7782,to_date('23-1-1982','dd-mm-yyyy'),1300,NULL,10);
COMMIT;
---Analytic examples
----Average salary by department
SELECT empno, deptno, sal,
       Round(AVG(sal) OVER (PARTITION BY deptno  ),2) AS avg_dept_sal
      
FROM   emp  where deptno=10;
order by deptno, empno,  sal ;
/* Adding order by sal in the partition by clause gives moving average*/
----Running total 

SELECT empno, deptno, sal,
       Round(sum(sal) OVER (order by empno),2) AS Running_sal
FROM   emp  ;
---Running total in a group
SELECT empno, deptno, sal,
       Round(sum(sal) OVER (partition by deptno order by empno ),2) AS Running_sal
FROM   emp  ;
--------Row numbering
select empno, deptno, 
       row_number() over ( order by deptno ) rn ,
       rank() over ( order by deptno ) rk, 
       dense_rank() over ( order by deptno ) dr from   emp  order by deptno,empno;
--previous and next value
select empno,sal,
       lag ( sal ) over ( order by empno ) prev_sal,
       lead ( sal ) over ( order by empno ) next_sal from   emp;
--first value and last value
select empno, deptno,sal,
first_value(sal) over (order by deptno) as first_sal,
last_value(sal) over (order by deptno) as last_sal
from emp order by deptno, sal;