pragma solidity ^0.4.18;

contract BlockSSL {

    struct certificateInfo {
        address creator;
        string domain;
        string uPortID;
        string certificateHash;
        uint serialNumber;
        uint expiry;
        string certDownloadLink;
    }

    mapping (address => certificateInfo) certificates;
    address[] public certAdd;

    event certificateInfoAdded(address creator, string domain, string uPortID, string certificateHash, uint serialNumber, uint expiry, string certDownloadLink);

    function setCertificate(address _address, address _creator, string _domain, string _uPortID, string _certificateHash, uint _serialNumber, uint _expiry, string _certDownloadLink) public {
        var certificatesInfo = certificates[_address];

        certificatesInfo.creator = _creator;
        certificatesInfo.domain = _domain;
        certificatesInfo.uPortID = _uPortID;
        certificatesInfo.certificateHash = _certificateHash;
        certificatesInfo.serialNumber = _serialNumber;
        certificatesInfo.expiry = _expiry;
        certificatesInfo.certDownloadLink = _certDownloadLink;

        certAdd.push(_address) -1;
        certificateInfoAdded(_creator, _domain, _uPortID, _certificateHash, _serialNumber, _expiry, _certDownloadLink);
    }

    function getCertificatesInfo() view public returns (address[]) { //Get all the info that has been added
        return certAdd;
    }

    function getCertificateInfo(address cert) view public returns (address, string, string, string, uint, uint, string) { //Get info of a specified address
        return (certificates[cert].creator, certificates[cert].domain, certificates[cert].uPortID, certificates[cert].certificateHash, certificates[cert].serialNumber, certificates[cert].expiry, certificates[cert].certDownloadLink);
    }

    function countCertificates() view public returns (uint){ //Count how many users create certificates
      return certAdd.length;
    }
}
