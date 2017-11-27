pragma solidity ^0.4.18;

contract BlockSSL {

    struct certificateInfo {
        address creator;
        string uPortID;
        string certificateHash;
        uint serialNumber;
        uint expiry;
    }

    mapping (address => certificateInfo) certificates;
    address[] public certAdd;

    event certificateInfoAdded(address creator, string uPortID, string certificateHash, uint serialNumber, uint expiry);

    function setCertificate(address _address, address _creator, string _uPortID, string _certificateHash, uint _serialNumber, uint _expiry) public {
        var certificatesInfo = certificates[_address];

        certificatesInfo.creator = _creator;
        certificatesInfo.uPortID = _uPortID;
        certificatesInfo.certificateHash = _certificateHash;
        certificatesInfo.serialNumber = _serialNumber;
        certificatesInfo.expiry = _expiry;

        certAdd.push(_address) -1;
        certificateInfoAdded(_creator, _uPortID, _certificateHash, _serialNumber, _expiry);
    }

    function getCertificatesInfo() view public returns (address[]) { //Get all the info that has been added
        return certAdd;
    }

    function getCertificateInfo(address cert) view public returns (address, string, string, uint, uint) { //Get info of a specified address
        return (certificates[cert].creator, certificates[cert].uPortID, certificates[cert].certificateHash, certificates[cert].serialNumber, certificates[cert].expiry);
    }

    function countCertificates() view public returns (uint){ //Count how many users create certificates
      return certAdd.length;
    }
}
