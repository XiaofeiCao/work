## Goal
### Long-term
Cover all cases for ARM templates
  - Cover existing ARM templates
  - Cover new ARM templates on the go
  - Detect breaking changes for ARM templates for new versions

### Short-term
1. Cover existing common ARM patterns
2. Cover GA lib cases

## Non-goal
Ensure backward compatibility


## Folder structure
### Proposal 1(current)
1. According to the ARM template categories, basically [this issue](https://github.com/Azure/cadl-ranch/issues/585)
```
Azure
 |-> ResourceManager
       |-> Models
             |-> Resources // resources and their common CRUD operations
             |-> CommonTypes // special common-types like ManagedIdentity
                |-> ManagedIdentities
                |-> EncryptionProperties
                |-> SKUs, etc
       |-> Operations // uncommon operations, or operations with multiple scenarios, irrelavant of resource types
             |-> LROs
             |-> Pageables
             |-> Resource Actions //import, export, upload, trigger, etc
             |-> Resource Move // move resource to another subscription(not sure, maybe just in Resources is enough?)
```

2. Flatten the hierarchy, only Resources
```
Azure
 |-> ResourceManager
       |-> Resources
             |-> Tracked
             |-> Proxy
             |-> Singleton
             |-> Mixed // put all corner cases here
```
