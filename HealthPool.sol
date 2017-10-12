pragma solidity ^0.4.2;

contract HealthPool{

  //GLOBALS
  uint256 total_funds = 0;

  //anyone should be able to access
  function getTotalFunds() constant returns (uint256){
    return total_funds;
  }

  //PARTICIPANTS
  uint256 total_participants = 0;
  mapping (address => Participant) public participants;
  address[] public participant_addrs;
  struct Participant{
    address addr;
    uint256 id;
    string name;
    uint8 age;
    uint256 funds_paid;
    uint256 last_payment;
    bool registered;
  }

  //callable by anyone
  function getTotalParticipants() constant returns (uint256){
    return total_participants;
  }

  //who is allowed to register participants? then limit to this entity
  function registerParticipant(address _addr, string _name, uint8 _age){
    Participant storage p = participants[_addr];
    assert(!p.registered);

    participants[_addr] = Participant({addr: _addr, id: total_participants, name: _name, age: _age, funds_paid: 0, last_payment: 0, registered: true});
    participant_addrs.push(_addr);
    total_participants ++;
  }

  //only callable by the participant replace address param with msg.sender?
  function payFunds(address _addr, uint256 _payment){
    Participant storage p = participants[_addr];
    assert(p.registered);
    assert(msg.sender == _addr);

    participants[_addr].last_payment = _payment;
    participants[_addr].funds_paid += _payment;
    total_funds += _payment;
  }

  //anyone can access (name should not be included)
  function getParticipant(address _addr) constant returns (address, uint256, string, uint8, uint256, uint256, bool){
    Participant storage p = participants[_addr];
    return (p.addr, p.id, p.name, p.age, p.funds_paid, p.last_payment, p.registered);
  }

  //anyone can access
  function getParticipantAddresses() constant returns (address[]){
    return participant_addrs;
  }

}
