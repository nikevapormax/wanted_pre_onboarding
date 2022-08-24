# wanted_pre_onboarding
## 요구사항 분석
- 회사는 채용공고를 생성하고, 이에 사용자는 지원한다.
- 우선적으로 회사가 채용공고를 생성하고, 이 채용공고를 수정 • 조회 • 삭제할 수 있어야 한다.
- 사용자는 지원하기 전 회사의 채용공고를 상세히 볼 수 있으며, 해당 회사의 다른 채용공고를 확인할 수 있다. 

## 구현과정
- 해당 서비스를 구현하는 과정에서 `postman`을 활용해 데이터를 생성하고 쿼리를 날려 결과를 확인하였다.
### 채용공고 생성
- 채용공고를 생성하기 위해 필요한 데이터를 postman을 통해 백엔드 서버로 값을 보내준다. 
- 백엔드의 serializer의 기본 validator를 통해 해당 값들의 유효성을 검사한다. 
- 만약 유효성 검사를 통과하면 db에 공고를 생성하게 된다. 
   - 테스트 코드를 통해 실패하는 경우의 테스트를 진행하였다.
   
### 채용공고 수정
- 회사가 작성한 채용공고를 수정하기 위해 수정할 값들을 백엔드 서버로 보내준다. (이때 회사 id는 수정 불가)
- 회사의 id를 건드릴 수 있는 가능성이 있기에 custom validator를 사용해 회사 id를 제거하였다. 
- 회사 id가 제거되고 validator의 유효성 검사를 통과한 validated_data를 custom updater로 보내 데이터를 수정하였다. (partila=True를 통해 부분 수정 가능)
- 테스트 코드를 통해 실패하는 경우에 대한 테스트를 진행하였다.

### 채용공고 삭제
- 해당 기능을 구현하면서 url에 채용공고의 id를 담아 보낼 수도 있지만, 구현 당시에는 프론트에서 보내는 request에 공고의 id값을 담아 보내도 될 것 같다 판단해 request를 사용하였다. 
- 백엔드에서 받은 공고의 id 값을 사용해 쿼리를 날렸고, 결과가 있는 경우에 채용공고를 삭제할 수 있도록 하였다. 
- 해당 기능 또한 테스트 코드를 통해 테스트를 진행하였다. 

### 채용공고 조회
- 사용자가 모든 채용공고를 조회할 수 있도록 db에 있는 모든 채용공고를 보내주었다. 
- 해당 기능 또한 테스트 코드를 통해 테스트를 진행하였다. 

### 채용공고 검색 기능
- 특정 값을 쿼리 파라미터로 받는 것이 아닌 공고의 모든 값을 받을 수 있다고 생각하며 기능을 구현하였다. 
- 쿼리 파라미터의 값을 숫자와 문자 두 가지로 나누어 받는 것에 착안해 `try except`문을 사용해 기능을 구현하였다. 
   - 숫자의 경우, 회사의 아이디와 보상금이 있는데 현 상황으로는 보상금의 최저기준을 50만원이라 책정해 그 값을 기준으로 아이디와 보상금을 구분하였다. 
   - 문자의 경우, if 문을 사용해 쿼리를 날리고 해당 값이 있다면 serializer를 통해 데이터를 보내는 방식을 채택하였다. 
- 현재 코드가 굉장히 깔끔하지 못하다고 생각하며, 우선 데드라인을 맞추기 위해 기능구현을 최우선 순위로 고려하였다. 

### 채용공고 상세 페이지
- 사용자가 채용공고의 모든 내용을 볼 수 있도록 기능을 구현하였다. 
- 마찬가지로 serializer에 사용자가 선택한 채용공고의 id 값을 통해 찾은 값을 넣어주어 사용자에게 제시하도록 하였다. 
   - 이 경우에는 url로 채용공고의 id 값을 받도록 설계하였다. 
- 사용자가 채용공고를 확인할 때 채용공고를 낸 회사가 만든 다른 채용공고들도 볼 수 있도록 다른 채용공고의 id 값을 같이 보내주었다. 
   - filter를 사용해 쿼리셋을 불러오므로, values("id")를 통해 id들을 불러오고 현재 공고의 아이디와 다른 것들만 제시하도록 코드를 작성하였다. 